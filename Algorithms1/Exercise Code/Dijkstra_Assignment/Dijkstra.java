package Dijkstra;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map.Entry;

public class Dijkstra {

	private IndexedHeap  pq;	
	private static int edgeCount = 0;               //  Use this to give names to the edges.										
	private HashMap<String,Edge>  edges = new HashMap<String,Edge>();

	private HashMap<String,String>   parent;
	private HashMap<String,Double>   dist;  //  This is variable "d" in lecture notes
	private String 					 startingVertex;	
	
	HashSet<String>  setS      ;
	HashSet<String>  setVminusS;

	/*
	 * Run Dijkstra's algorithm from a vertex whose name is given by the string s.
	 */
	
	public void dijkstraVertices(Graph graph, String s){
		
		IndexedHeap 	pq    = new IndexedHeap()  ;
		
		setS       = new HashSet<String>();
		setVminusS = new HashSet<String>();
		
		parent  = new HashMap<String,String>();
		dist 	= new HashMap<String,Double>();

		//  temporary variables
		
		String min;
		
		double  distToU,
				costUV;		
		
		HashMap<String,Double>    uAdjList;		
		initialize(graph,s);
		
		parent.put( s, null );
		pq.add(s, 0.0);   // shortest path from s to s is 0.
		this.startingVertex = s;
		
		while (pq.isEmpty() == false){
			double minPri = pq.getMinPriority();
			//System.out.println(minPri);
			min = pq.removeMin();
			setS.add(min);
			dist.put(min, minPri);
			setVminusS.remove(min);
			
			HashMap<String, Double> al = graph.getAdjList().get(min);
			for (Entry<String, Double> e : al.entrySet()){
				
				if (setVminusS.contains(e.getKey()) ){
					//System.out.println("Test");
					parent.put(e.getKey(), min);
					distToU = dist.get(min);
					costUV = e.getValue();
					System.out.println(min + " " + Double.toString(costUV) + " " + Double.toString(distToU));
					
					if (pq.contains(e.getKey()) ){
						if (pq.getPriority(e.getKey()) > costUV + distToU ){
							pq.changePriority(e.getKey(), costUV + distToU);//get the cost from s to min and add to cost of crossing edge
						}
					}
					else{
						pq.add(e.getKey(), costUV + distToU);
					}
				}
			}
			
		}

	}
	
	
	public void dijkstraEdges(Graph graph, String startingVertex){

		//  Makes sets of the names of vertices,  rather than vertices themselves.
		//  (Could have done it either way.)
		
		setS       = new HashSet<String>();
		setVminusS = new HashSet<String>();
		pq    	   = new IndexedHeap();
		
		parent  = new HashMap<String,String>();
		dist 	= new HashMap<String,Double>();
		//  temporary variables
		
		initialize(graph, startingVertex);
		
		//Edge start = new Edge(edgeCount, startingVertex, startingVertex);
		//edges.put(start.edgeName, start);
		//edgeCount++;
		
		//pq.add(start.edgeName, 0);   // shortest path from s to s is 0.
		pqAddEdgesFrom(graph, startingVertex);
		
		while (pq.isEmpty() == false){
			double minPri = pq.getMinPriority();
			Edge tmp = edges.get( pq.removeMin() );
			//System.out.println(tmp.v + " " + (!(setS.contains(tmp.v))));
			if (!(setS.contains(tmp.v))){

				setS.add(tmp.v);
				
				if (tmp.v!=tmp.u){
					parent.put(tmp.v, tmp.u);
				}
				else{
					parent.put(tmp.v, null);
				}
				
				dist.put(tmp.v, minPri);
				setVminusS.remove(tmp.v);
				
				pqAddEdgesFrom(graph, tmp.v);
			
			}
		}

	}
		

	private void initialize(Graph graph, String startingVertex){
		//  initialization of sets V and VminusS,  dist, parent variables
		//

		for (String v : graph.getVertices()){
			setVminusS.add( v );
			dist.put(v, Double.POSITIVE_INFINITY);
			parent.put(v, null);
		}
		this.startingVertex = startingVertex;

		//   Transfer the starting vertex from VminusS to S and  

		setVminusS.remove(startingVertex);
		setS.add(startingVertex);
		dist.put(startingVertex, 0.0);
		parent.put(startingVertex, null);
	}

    /*  
	 *  helper method for dijkstraEdges:   Whenever we move a vertex u from V\S to S,  
	 *  add all edges (u,v) in E to the priority queue of edges.
	 *  
	 *  For each edge (u,v), if this edge gave a shorter total distance to v than any
	 *  previous paths that terminate at v,  then this edge will be removed from the priority
	 *  queue before these other vertices. 
	 *  
	 */
	
	public void pqAddEdgesFrom(Graph g, String u){
		System.out.println("edge added from " + u);
		
		double distToU = dist.get(u); 
		for (String v : g.getAdjList().get(u).keySet()  ){  //  all edges of form (u, v) 
			
			edgeCount++;
			Edge e = new Edge( edgeCount, u, v );
			edges.put( e.getName(), e );
			pq.add( e.getName() ,  distToU + g.getAdjList().get(u).get(v) );
		}
	}

	// -------------------------------------------------------------------------------------------
	
	public String toString(){
		String s = "";
		s += "\nRan Dijkstra from vertex " + startingVertex + "\n";
		for (String v : parent.keySet()){
			s += v + "'s parent is " +   parent.get(v) ;
			s += "   and pathlength is "  + dist.get(v) + "\n" ;
		}
		return s;
	}

	//  This class is used only to keep track of edges in the priority queue for dijkstraEdges().
	
	private class Edge{
		
		public String edgeName;
		public String u, v;
		
		Edge(int i, String u, String v){
			this.edgeName = "e_" + Integer.toString(i);
			this.u = u;
			this.v = v;
		}
		
		public String getName(){
			return edgeName;
		}
		
		String getStartVertex(){
			return u;
		}

		String getEndVertex(){
			return v;
		}
		
		public String toString(){
			return 	edgeName + " : " + u + " " + v;
		}
	}
	

}

