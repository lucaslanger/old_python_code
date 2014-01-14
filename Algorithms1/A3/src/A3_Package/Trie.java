package A3_Package;

import java.util.*;

//Trie class.  Each node is associated with a prefix of some key 
//stored in the trie.   (Note any string is a prefix of itself.)

public class Trie
{
	private TrieNode root;

	// Empty trie has just a root node.  All the children are null.

	public Trie() 
	{
		root = new TrieNode();
	}

	public TrieNode getRoot(){
		return root;
	}

	// Return true if key is contained in the trie (i.e. it was added by insert), false otherwise

	public boolean contains(String key)
	{  
		
		TrieNode cNode = this.getRoot();
		for (int c=0;c<key.length();c++){
			TrieNode cChild = cNode.getChild((char) key.charAt(c));
			if (cChild == null){
				return false;
			}
			else{
				cNode = cChild;	
			}
		}
		
		return cNode.isEndOfKey();
	}

	// Insert key into the trie.  The first step should be finding the longest 
	// prefix of key already in the trie (use getPrefixNode() below).  
	// Then add TrieNodes in such a way that the key is inserted.

	public void insert(String key)
	{
		TrieNode prevchar = this.getRoot();
		
		for (int c=0;c<key.length();c++ ){
			if (prevchar.getChild((char) key.charAt(c)) == null){
				prevchar.createChild((char) key.charAt(c));
			}
			prevchar = prevchar.getChild((char) key.charAt(c));
			if (c == key.length() - 1){
				prevchar.setEndOfKey(true);
			}
		}
		

	}

	// insert each key in the list (keys)

	public void loadKeys(ArrayList<String> keys)
	{
		for (int i = 0; i < keys.size(); i++)
		{
			System.out.println("Inserting " + keys.get(i));
			insert(keys.get(i));
		}
		return;
	}

	// Return the TrieNode corresponding the longest prefix of a key that is found. 
	// If no prefix is found, return the root. 
	// In the example in the PDF, running getPrefixNode("any") should return the
	// dashed node under "n", since "an" is the longest prefix of "any" in the trie. 
	// getPrefixNode("addition") should return the node which is the first 
	// child of the root since "a" is the longest prefix of "addition" in the trie.

	private TrieNode getPrefixNode(String word)
	{
		TrieNode longestPrefix = this.getRoot();
		for (int c=0;c<word.length();c++){			
			TrieNode cChild = longestPrefix.getChild((char) word.charAt(c));
			if (cChild == null){
				return longestPrefix;
			}
			else{
			longestPrefix = cChild;
				
			}
		}
		return longestPrefix;
	}
	
	
	private TrieNode getPrefixNodeThatIsKey(String word)
	{
		TrieNode longestPrefix = this.getRoot();
		TrieNode currentpos = this.getRoot();
		for (int c=0;c<word.length();c++){
			try{
			TrieNode cChild = currentpos.getChild((char) word.charAt(c));
			if (cChild.isEndOfKey()){
				longestPrefix = cChild;
			}
			currentpos = cChild;
				
			}
			catch(Exception e){
				return longestPrefix;
			}
		}
		return longestPrefix;
	}

	// Similar to getPrefixNode() but now return the prefix as a String, 
	// rather than as a TrieNode.   

	public String getPrefix(String word)
	{
		String s = getPrefixNode(word).toString();
		if (s == null){
			return "";
		}
		else{
			return s;
		}
	}


	// Return a list of all keys in the trie that have the given prefix.  
	// If there are no matches, then return an empty list.
	// (Or you can return null -- since the original posting of this code said
	//  that's what you should do (in the AutoComplete class).

	public ArrayList<String> getAllPrefixMatches( String prefix )
	{
		ArrayList<String> matches = new ArrayList<String>(10);
		TrieNode pref = getPrefixNode(prefix);
		ArrayList<Character> childchars = pref.getChildren();
		
		if (pref.getParent() == null){ //THIS TESTS TO SEE IF THE NEXT LETTER OF THE PREFIX IS NOT IN THE TREE
			return matches;            //IF AT ANY POINT IN PREFIX THERE IS A LETTER THAT ISNT IN THE TREE (ON THAT PATH) GETPREFIX WILL RETURN THE ROOT, WHICH CAUSES THIS TO FAIL
		}
		
		//NO NEED FOR A BASE CASE BECAUSE IF CHILDCHARS.SIZE == 0 THEN LOOP DOESN'T ITERATE! 
		
		else{
			for (int i=0;i<childchars.size();i++){
				if (pref.getChild(childchars.get(i)).isEndOfKey()){
					matches.add(prefix + childchars.get(i));// Would be redundant to add prefix in base case because you do so right here
				}
				ArrayList<String> childmatches = getAllPrefixMatches(prefix + childchars.get(i));
				int j=0;
				while (j<childmatches.size()){
					matches.add(childmatches.get(j));
					j++;
				}
				j=0;
			}
			return matches;
		}
	}
		
		
}
