package Indexer;

import java.io.File;
import java.io.FileFilter;
import java.io.FileReader;
import java.io.IOException;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

public class Indexer {

	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception {
		// all paths are relative to eclipse's base path
		String dataDir = "../../static/2-Feeds";
		String indexDir = "../../static/3-Index";

		// make sure the index dir exists
		new File(dataDir).mkdir();

		long start = System.currentTimeMillis();
		Indexer indexer = new Indexer(indexDir);
		int numIndexed;
		try {
			numIndexed = indexer.index(dataDir, new TextFilesFilter());
		} 
		finally {
			indexer.close();
		}
		long end = System.currentTimeMillis();

		System.out.println("Indexing " + numIndexed + " files took "+ (end - start) + " milliseconds");
	}

	private IndexWriter writer;

	public Indexer(String indexDir) throws IOException {
		Directory dir = FSDirectory.open(new File(indexDir));
		writer = new IndexWriter(dir, 							//3
				new StandardAnalyzer( 							//3
						Version.LUCENE_CURRENT),				//3
						true, 									//3
						IndexWriter.MaxFieldLength.UNLIMITED);  //3
	}

	public void close() throws IOException {
		writer.close(); //4
	}

	public int index(String dataDir, FileFilter filter) 
	throws Exception {

		File[] files = new File(dataDir).listFiles();

		for (File f: files) {
			if (!f.isDirectory() &&
					!f.isHidden() &&
					f.exists() &&
					f.canRead() &&
					(filter == null || filter.accept(f))) {
				indexFile(f);
			}
		}
		return writer.numDocs(); //5
	}

	private static class TextFilesFilter implements FileFilter {
		public boolean accept(File path) {
			if (path==null) {
				path = new File("/home/mike/workspace/PodSearch/static/2-Feeds");
			}
			return path.getName().toLowerCase() //6
			.endsWith(".rss"); 					//6
		}
	}

	protected Document getDocument(File f) throws Exception {
		Document doc = new Document();
		doc.add(new Field("contents", new FileReader(f))); //7
		doc.add(new Field("filename", f.getName(), //8
				Field.Store.YES, Field.Index.NOT_ANALYZED));//8
		doc.add(new Field("fullpath", f.getCanonicalPath(), //9
				Field.Store.YES, Field.Index.NOT_ANALYZED));//9
		return doc;
	}

	private void indexFile(File f) throws Exception {
		System.out.println("Indexing " + f.getCanonicalPath());
		Document doc = getDocument(f);
		writer.addDocument(doc); //10
	}
}
