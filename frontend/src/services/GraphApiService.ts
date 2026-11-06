import type { GraphResponse } from "../models/Graph";

function isGraphResponse(value: unknown): value is GraphResponse {
  if (typeof value !== "object" || value === null) return false;
  const graph = value as Partial<GraphResponse>;
  return (
    typeof graph.query === "string" &&
    Array.isArray(graph.nodes) &&
    Array.isArray(graph.edges) &&
    typeof graph.total_matches === "number" &&
    typeof graph.truncated === "boolean"
  );
}

export async function fetchGraph(query: string): Promise<GraphResponse> {
  const params = new URLSearchParams({ q: query });
  const response = await fetch(`/api/v1/graph?${params.toString()}`);
  const body: unknown = await response.json().catch(() => null);

  if (!response.ok) {
    if (response.status === 503) {
      throw new Error(
        "Os dados do grafo ainda não estão disponíveis. Prepare os arquivos de dados e tente novamente.",
      );
    }
    if (response.status === 422) {
      throw new Error("A busca não é válida. Revise o termo e tente novamente.");
    }
    throw new Error(
      `Não foi possível buscar o grafo (erro ${response.status}). Tente novamente.`,
    );
  }

  if (!isGraphResponse(body)) {
    throw new Error("A API retornou uma resposta inesperada para o grafo.");
  }

  return body;
}
