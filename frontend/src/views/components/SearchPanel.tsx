import type { FormEvent } from "react";

interface SearchPanelProps {
  query: string;
  loading: boolean;
  onQueryChange: (query: string) => void;
  onSearch: (query: string) => void;
}

export function SearchPanel({
  query,
  loading,
  onQueryChange,
  onSearch,
}: SearchPanelProps) {
  const submit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    onSearch(query);
  };

  return (
    <aside className="search-panel">
      <div className="eyebrow"><span className="eyebrow-dot" /> EXPLORADOR DE PESQUISA</div>
      <h1>Siga o caminho<br />de uma ideia.</h1>
      <p className="intro">
        Encontre um artigo e explore as pesquisas relacionadas por meio das citações.
      </p>

      <form className="search-form" onSubmit={submit}>
        <label htmlFor="paper-search">Buscar artigos</label>
        <div className="search-field">
          <svg viewBox="0 0 20 20" aria-hidden="true">
            <circle cx="8.5" cy="8.5" r="5.5" />
            <path d="m13 13 4 4" />
          </svg>
          <input
            id="paper-search"
            maxLength={200}
            onChange={(event) => onQueryChange(event.target.value)}
            placeholder="Ex.: quantum field theory"
            value={query}
          />
          <kbd>↵</kbd>
        </div>
        <button className="search-button" disabled={loading} type="submit">
          {loading ? <span className="spinner" /> : "Explorar grafo"}
          {!loading && <span aria-hidden="true">→</span>}
        </button>
        <p className="search-hint">Busque por título, autor, assunto ou resumo.</p>
      </form>

      <div className="search-footer">
        <span className="footer-icon" aria-hidden="true">⌘</span>
        <span>Cada conexão conta parte da história.</span>
      </div>
    </aside>
  );
}
