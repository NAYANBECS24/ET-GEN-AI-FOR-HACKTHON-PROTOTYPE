import axios from "axios";

export interface VerifyResponse {
  package: string;
  intent: string;
  hallucination: boolean;
  reputation: number;
  alternative?: string | null;
}

export class AegisClient {
  constructor(private baseUrl: string, private token?: string) {}

  async verifyPackage(packageName: string, code: string): Promise<VerifyResponse> {
    const res = await axios.post(
      `${this.baseUrl}/api/v1/package/verify`,
      { package_name: packageName, context_code: code, development_context: {} },
      { headers: this.token ? { Authorization: `Bearer ${this.token}` } : {} }
    );
    return res.data as VerifyResponse;
  }
}
