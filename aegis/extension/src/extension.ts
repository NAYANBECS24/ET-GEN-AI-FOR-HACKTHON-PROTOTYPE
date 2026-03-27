import * as vscode from "vscode";
import { AegisClient } from "./api/client";
import { detectImports } from "./analyzers/importAnalyzer";
import { SecurityCodeLensProvider, SecurityHoverProvider } from "./providers/securityProvider";

export function activate(context: vscode.ExtensionContext) {
  const cfg = vscode.workspace.getConfiguration("aegis");
  const baseUrl = cfg.get<string>("backendUrl", "http://localhost:8000");
  const token = cfg.get<string>("token", "");
  const client = new AegisClient(baseUrl, token);

  const codeLensProvider = new SecurityCodeLensProvider();
  context.subscriptions.push(
    vscode.languages.registerCodeLensProvider([{ language: "python" }, { language: "typescript" }, { language: "javascript" }], codeLensProvider)
  );
  context.subscriptions.push(vscode.languages.registerHoverProvider("*", new SecurityHoverProvider()));

  const verifyDocument = async (document: vscode.TextDocument) => {
    const text = document.getText();
    const imports = detectImports(text);
    const lenses: vscode.CodeLens[] = [];

    for (const pkg of imports) {
      try {
        const verdict = await client.verifyPackage(pkg, text);
        if (verdict.hallucination) {
          const line = document.lineAt(0);
          const cmd: vscode.Command = {
            title: `AEGIS: Replace ${pkg} with ${verdict.alternative ?? "trusted package"}`,
            command: "aegis.verifyCurrentFile"
          };
          lenses.push(new vscode.CodeLens(line.range, cmd));
          vscode.window.showWarningMessage(`AEGIS blocked suspicious package '${pkg}'. Suggested: ${verdict.alternative ?? "review manually"}`);
        }
      } catch (err) {
        console.error("AEGIS verify failed", err);
      }
    }

    codeLensProvider.setLenses(lenses);
  };

  context.subscriptions.push(vscode.workspace.onDidChangeTextDocument((e) => verifyDocument(e.document)));
  context.subscriptions.push(vscode.commands.registerCommand("aegis.verifyCurrentFile", async () => {
    const doc = vscode.window.activeTextEditor?.document;
    if (doc) await verifyDocument(doc);
  }));
}

export function deactivate() {
  // noop
}
