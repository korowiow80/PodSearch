package Searcher;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;

import java.io.IOException;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.queryParser.ParseException;
import org.apache.lucene.queryParser.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

public class Searcher {
	public static void main(String[] args) throws Exception {
		String indexDir = "../../static/3-Index";					//1
		String q = "";  										//2	
		// Read the query from the console
		try {
			BufferedReader in = new BufferedReader(new InputStreamReader(System.in));

			System.out.print("Search: ");
			q = in.readLine();
		} 
		catch (IOException e) {
		}

		search(indexDir, q);
	}

	public static void search(String indexDir, String q)
			throws IOException, ParseException {

		Directory dir = FSDirectory.open(new File(indexDir)); 		//3
		IndexSearcher is = new IndexSearcher(dir);					//3

		QueryParser parser = new QueryParser(Version.LUCENE_CURRENT, //4
				"contents", 							 //4
				new StandardAnalyzer(					 //4						
						Version.LUCENE_CURRENT)); 				 //4

		Query query = parser.parse(q);						 //4
		long start = System.currentTimeMillis();
		TopDocs hits = is.search(query, 10); 				 //5
		long end = System.currentTimeMillis();

		System.err.println("Found " + hits.totalHits +		 //6
				" document(s) (in " + (end - start) +		 //6
				" milliseconds) that matched query '" +		 //6
				q + "':");									 //6

		for(int i=0;i<hits.scoreDocs.length;i++) {
			ScoreDoc scoreDoc = hits.scoreDocs[i];		 //7
			Document doc = is.doc(scoreDoc.doc);		 //7

			System.out.println(doc.get("filename"));	 //8
		}

		is.close(); 										 //9	
	}
}

