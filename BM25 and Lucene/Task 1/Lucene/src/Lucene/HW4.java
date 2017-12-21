package Lucene;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.*;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

import java.io.*;
import java.util.ArrayList;
import java.util.Scanner;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */
public class HW4 {
    private static Analyzer analyzer = new SimpleAnalyzer(Version.LUCENE_47);

    private IndexWriter writer;
    private ArrayList<File> queue = new ArrayList<File>();

    public static void main(String[] args) throws IOException {
        System.out
                .println("Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\\temp\\index)");

        String indexLocation = null;
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();

        HW4 indexer = null;
        try {
            indexLocation = s;
            indexer = new HW4(s);
        } catch (Exception ex) {
            System.out.println("Cannot create index..." + ex.getMessage());
            System.exit(-1);
        }

        // ===================================================
        // read input from user until he enters q for quit
        // ===================================================
        while (!s.equalsIgnoreCase("q")) {
            try {
                System.out
                        .println("Enter the FULL path to add into the index (q=quit): (e.g. /home/mydir/docs or c:\\Users\\mydir\\docs)");
                System.out
                        .println("[Acceptable file types: .xml, .html, .html, .txt]");
                s = br.readLine();
                if (s.equalsIgnoreCase("q")) {
                    break;
                }

                // try to add file into the index
                indexer.indexFileOrDirectory(s);
            } catch (Exception e) {
                System.out.println("Error indexing " + s + " : "
                        + e.getMessage());
            }
        }

        // ===================================================
        // after adding, we always have to call the
        // closeIndex, otherwise the index is not created
        // ===================================================
        indexer.closeIndex();

        // =========================================================
        // Now search
        // =========================================================

        // Edited by Sanjay Murali to read the file containing the queries and create file for top 100 results for each

        IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(
                indexLocation)));
        IndexSearcher searcher = new IndexSearcher(reader);
        TopScoreDocCollector collector = null;

        String pathToQueryList = "QueryList.txt"; // File containing the queries

        BufferedReader brnew = new BufferedReader(new InputStreamReader(System.in));
        System.out.println("Enter Path to Query List file (skip for default): ");
        String path = brnew.readLine();
        if(!path.equals("")){
            pathToQueryList = path;
        }

        File pointerToQueries = new File(pathToQueryList); // pointer to file
        Scanner fileContent = null;
        FileWriter outputStream = null;

        // create folder for placing Lucene result
        File folderSetup = new File("DOC List Rank Lucene");
        File[] files = folderSetup.listFiles();
        if (files != null) {
            for (File file : files) {
                if (file.isDirectory()) {
                    File[] insidefiles = file.listFiles();
                    for (File insidefile : insidefiles) {
                        insidefile.delete();
                    }
                }
                file.delete();
            }
        }
        folderSetup.delete();
        folderSetup.mkdir();


        int query_ID = 1;

        // check if Query List file exists
        if (pointerToQueries.exists()) {
            try {
                // start reading contents of the file
                fileContent = new Scanner(pointerToQueries);
                while (fileContent.hasNextLine()) {
                    String query = fileContent.nextLine();

                    collector = TopScoreDocCollector.create(1000, true);
                    Query q = new QueryParser(Version.LUCENE_47, "contents", analyzer).parse(query);
                    searcher.search(q, collector);
                    ScoreDoc[] hits = collector.topDocs().scoreDocs;
                    System.out.println(query + " " + hits.length);
                    int maxResults = Math.min(100, hits.length); // Return only top 100 results
                    try {
                        outputStream = new FileWriter("DOC List Rank Lucene/Q" + query_ID + ".txt");
                        String builder = "";
                        for (int i = 0; i < maxResults; i++) {
                            int docId = hits[i].doc;
                            Document d = searcher.doc(docId);
                            String fileName = d.get("filename"); // get file name
                            fileName = fileName.substring(0, fileName.length() - 4); // removing extension

                            // Output form : Query_ID Q0 fileName docID Rank score Lucene
                            builder += query_ID + " Q0 " + fileName + " " + docId + " "
                                    + (i + 1) + " " + hits[i].score + " Lucene\n";
                        }
                        builder = builder.substring(0, builder.length()-1); // remove trailing new line "\n"
                        outputStream.write(builder);
                    } finally {
                        outputStream.close();
                    }
                    query_ID++;
                }


            } catch (Exception e) {
                System.out.println("Exception Occurred in reading Query List File!");
                e.printStackTrace();
            } finally {
                fileContent.close();
            }

        }

    System.out.println("Check DOC List Rank Lucene folder for scores");
    }

    /**
     * Constructor
     *
     * @param indexDir the name of the folder in which the index should be created
     * @throws java.io.IOException when exception creating index.
     */
    HW4(String indexDir) throws IOException {

        FSDirectory dir = FSDirectory.open(new File(indexDir));

        IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47,
                analyzer);

        writer = new IndexWriter(dir, config);
    }

    /**
     * Indexes a file or directory
     *
     * @param fileName the name of a text file or a folder we wish to add to the
     *                 index
     * @throws java.io.IOException when exception
     */
    public void indexFileOrDirectory(String fileName) throws IOException {
        // ===================================================
        // gets the list of files in a folder (if user has submitted
        // the name of a folder) or gets a single file name (is user
        // has submitted only the file name)
        // ===================================================
        addFiles(new File(fileName));

        int originalNumDocs = writer.numDocs();
        for (File f : queue) {
            FileReader fr = null;
            try {
                Document doc = new Document();

                // ===================================================
                // add contents of file
                // ===================================================
                fr = new FileReader(f);
                doc.add(new TextField("contents", fr));
                doc.add(new StringField("path", f.getPath(), Field.Store.YES));
                doc.add(new StringField("filename", f.getName(),
                        Field.Store.YES));

                writer.addDocument(doc);
                System.out.println("Added: " + f);
            } catch (Exception e) {
                System.out.println("Could not add: " + f);
            } finally {
                fr.close();
            }
        }

        int newNumDocs = writer.numDocs();
        System.out.println("");
        System.out.println("************************");
        System.out
                .println((newNumDocs - originalNumDocs) + " documents added.");
        System.out.println("************************");

        queue.clear();
    }

    private void addFiles(File file) {

        if (!file.exists()) {
            System.out.println(file + " does not exist.");
        }
        if (file.isDirectory()) {
            for (File f : file.listFiles()) {
                addFiles(f);
            }
        } else {
            String filename = file.getName().toLowerCase();
            // ===================================================
            // Only index text files
            // ===================================================
            if (filename.endsWith(".htm") || filename.endsWith(".html")
                    || filename.endsWith(".xml") || filename.endsWith(".txt")) {
                queue.add(file);
            } else {
                System.out.println("Skipped " + filename);
            }
        }
    }

    /**
     * Close the index.
     *
     * @throws java.io.IOException when exception closing
     */
    public void closeIndex() throws IOException {
        writer.close();
    }
}