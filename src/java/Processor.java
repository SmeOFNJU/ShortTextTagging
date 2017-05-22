package test;

import java.io.File;
import java.io.IOException;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class Processor {
	
	private final String input = "./input";
	private final String output = "./output";
	
	public void processQuestion(File input){
		
	}
	public void processTopic(File input){
		try {
			Document doc = Jsoup.parse(input, "UTF-8");
			Elements divs = doc.select("div[class=feed-item feed-item-hook question-item]");
			for(Element div : divs){
				Elements questions = div.select("a[class=question_link]");
				String questionLink = "";
				if(questions.size() > 0){
					questionLink = questions.get(0).attr("href");
				}
				
				Elements subtopicdiv = div.select("div[class=subtopic]");
				Elements subtopics = subtopicdiv.select("a");
				String subtopicName = "";
				if(subtopics.size() > 0){
					subtopicName = subtopics.get(0).text();
				}
			}

		} catch (IOException e) {
			e.printStackTrace();
			Log.getLogger().info("Exception : " + e.toString());
		}
	}
	
	
	public void traverseFiles(File root){
		if(root.exists()){
			File[] files = root.listFiles();
			for(File file : files){
				if(file.isDirectory()){
					traverseFiles(file);
				}else{
					if(!file.getName().contains("question")){
						processTopic(file);
					}
				}
			}
		}
	}
	
	public static void main(String[] args){
		
	}
}
