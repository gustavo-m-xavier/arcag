import { useCallback, useRef, useState } from "react";
import type { GraphNode, GraphResponse } from "../models/Graph";
import { fetchGraph } from "../services/GraphApiService";

export function useGraphExplorerViewModel() {
  const [query, setQuery] = useState("");
  const [graph, setGraph] = useState<GraphResponse | null>(null);
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const requestId = useRef(0);

  const search = useCallback(async (searchTerm: string) => {
    const normalizedQuery = searchTerm.trim();
    if (!normalizedQuery) {
      setError("Digite um título, autor, assunto ou palavra-chave para buscar.");
      return;
    }

    const currentRequestId = ++requestId.current;
    setLoading(true);
    setError(null);
    setSelectedNode(null);

    try {
      const result = await fetchGraph(normalizedQuery);
      if (currentRequestId === requestId.current) setGraph(result);
    } catch (requestError) {
      if (currentRequestId !== requestId.current) return;
      setGraph(null);
      setError(
        requestError instanceof TypeError
          ? "Não foi possível conectar à API. Verifique se o servidor está em execução e tente novamente."
          : requestError instanceof Error
            ? requestError.message
            : "Não foi possível carregar o grafo de citações. Tente novamente.",
      );
    } finally {
      if (currentRequestId === requestId.current) setLoading(false);
    }
  }, []);

  const searchSuggestion = useCallback((suggestion: string) => {
    setQuery(suggestion);
    void search(suggestion);
  }, [search]);

  const selectNode = useCallback((node: GraphNode | null) => {
    setSelectedNode(node);
  }, []);

  const reportError = useCallback((message: string) => {
    setError(message);
  }, []);

  return {
    query,
    setQuery,
    graph,
    selectedNode,
    loading,
    error,
    search,
    searchSuggestion,
    selectNode,
    reportError,
  };
}
