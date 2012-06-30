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

	private IndexWriter writer;
	
	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception {
		// all paths are relative to eclipse's base path
		String dataDir = "../../static/2-Feeds";
		String indexDir = "../../static/3-Index";

		// Logging
		String indexDirAbsPath = new File(indexDir).getAbsolutePath();
		System.out.println("IndexDir: " + indexDirAbsPath);
		String dataDirAbsPath = new File(dataDir).getAbsolutePath();
		System.out.println("DataDir: " + dataDirAbsPath);
		
		// make sure the index directory exists
		new File(indexDir).mkdir();

		long start = System.currentTimeMillis();
		Indexer indexer = new Indexer(indexDir);
		int numIndexed;
		try {
			// numIndexed = indexer.index(dataDir, new TextFilesFilter());
			numIndexed = indexer.index(dataDir, new MediaFilesFilter());
		} 
		finally {
			indexer.close();
		}
		long end = System.currentTimeMillis();

		System.out.println("Indexing " + numIndexed + " files took "+ (end - start) + " milliseconds");
	}

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

	public int index(String dataDir, FileFilter filter) throws Exception {

		File[] files = new File(dataDir).listFiles();

		for (File f: files) {
			System.out.println("Path: " + f.getPath());
			if (f.isDirectory()) {
				this.index(f.getPath(), filter);
				continue;
			}
			if (f.isHidden()) continue;
			if (!f.exists()) continue;
			if (!f.canRead()) continue;
			if (filter != null && !filter.accept(f)) continue;
			indexFile(f);
		}
		return writer.numDocs(); //5
	}

	private static class TextFilesFilter implements FileFilter {
		public boolean accept(File path) {
			boolean accepted = false;
			if (path.getName().toLowerCase().endsWith(".atom")) {
				accepted = true;
			}
			if (path.getName().toLowerCase().endsWith(".rss")) {
				accepted = true;
			}
			if (path.getName().toLowerCase().endsWith(".xml")) {
				accepted = true;
			}
			return accepted;
		}
	}

	/* Filters obvious media files by file name extension */
	private static class MediaFilesFilter implements FileFilter {
		public boolean accept(File path) {
			boolean accepted = true;
			if (path.getName().toLowerCase().endsWith(".mp3")) accepted = false;
			if (path.getName().toLowerCase().endsWith(".ogg")) accepted = false;
			if (path.getName().toLowerCase().endsWith(".avi")) accepted = false;
			if (path.getName().toLowerCase().endsWith(".wma")) accepted = false;
			if (path.getName().toLowerCase().endsWith(".wmv")) accepted = false;
			if (path.getName().toLowerCase().endsWith(".mov")) accepted = false;
			return accepted;
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
