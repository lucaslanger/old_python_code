package Dijkstra;

public class TestDijkstra{
	public static void main(String[] args) {
		
		Graph graph;

		Dijkstra dijkstra = new Dijkstra();
		
		/*
		GraphReader  reader	=	new GraphReader("src/a2posted/test_graph_1.sdot");
		String startingVertex = "4";
		*/
		GraphReader  reader	=	new GraphReader("Graphs/test_graph_2.sdot");
		String startingVertex = "a";
		graph = reader.getParsedGraph();
		
		dijkstra.dijkstraVertices( graph, startingVertex );
		System.out.println("dijkstraVertices: \n" + dijkstra.toString() );
		
		dijkstra.dijkstraEdges(    graph, startingVertex );
		System.out.println("dijkstraEdges: \n" + dijkstra );
	}
}