import { GraphExplorerView } from "./views/GraphExplorerView";
import { useGraphExplorerViewModel } from "./viewmodels/useGraphExplorerViewModel";

function App() {
  const viewModel = useGraphExplorerViewModel();
  return <GraphExplorerView viewModel={viewModel} />;
}

export default App;
