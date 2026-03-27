const IMPORT_RE = /(?:import|from)\s+([@a-zA-Z0-9_\-/.]+)/g;

export function detectImports(source: string): string[] {
  const found = new Set<string>();
  let m: RegExpExecArray | null;
  while ((m = IMPORT_RE.exec(source)) !== null) {
    found.add(m[1].split(".")[0]);
  }
  return [...found];
}
