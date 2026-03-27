import * as vscode from "vscode";

export class SecurityCodeLensProvider implements vscode.CodeLensProvider {
  private lenses: vscode.CodeLens[] = [];

  setLenses(lenses: vscode.CodeLens[]) {
    this.lenses = lenses;
  }

  provideCodeLenses(): vscode.ProviderResult<vscode.CodeLens[]> {
    return this.lenses;
  }
}

export class SecurityHoverProvider implements vscode.HoverProvider {
  provideHover(document: vscode.TextDocument, position: vscode.Position): vscode.ProviderResult<vscode.Hover> {
    const range = document.getWordRangeAtPosition(position);
    if (!range) {
      return;
    }
    const word = document.getText(range);
    return new vscode.Hover(`AEGIS security context for package: **${word}**`);
  }
}
