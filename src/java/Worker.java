package test;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.MalformedURLException;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.TimeUnit;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import com.gargoylesoftware.htmlunit.FailingHttpStatusCodeException;
import com.gargoylesoftware.htmlunit.Page;
import com.gargoylesoftware.htmlunit.WebClient;
import com.gargoylesoftware.htmlunit.WebResponse;

public class Worker implements Runnable{
	
	private int curPage;
	private WebClient client;
	private String topicLink;
	private BlockingQueue<String> topicQueue;
	private ConcurrentHashMap<String, String> topicMap;
	private String dirName;
	private String topicName;
	
	private final String prefix = "http://www.zhihu.com";
	private final String suffix = "/questions?page=";
	
	public Worker(int curPage, String topicLink, BlockingQueue<String> topicQueue, 
			ConcurrentHashMap<String, String> topicMap, String topicName){
		this.curPage = curPage;
		this.client = create();
		this.topicLink = topicLink;
		this.topicQueue = topicQueue;
		this.topicMap = topicMap;
		this.dirName = "./data/" + topicName;
		this.topicName = topicName;
	}
	
	public WebClient create(){
		WebClient client = new WebClient();
		client.getOptions().setJavaScriptEnabled(false);
		client.getOptions().setCssEnabled(false);
		client.getOptions().setThrowExceptionOnFailingStatusCode(false);
		return client;
	}
	
	//http://www.zhihu.com/topic/19551137/questions?page=2
	public void writeQuestion(String dirName, String url, String html){
		String[] fields = url.split("[/]");
		if(fields.length < 6)
			return;
		String[] pnum = fields[5].split("[?]");
		if(pnum.length < 2)
			return;
		String fileName = dirName + "/" + fields[3] + " " + fields[4] + " " + pnum[1];
		File file = new File(fileName);
    	if(file.exists()){
    		return;
    	}else{
    		try {
				file.createNewFile();
			} catch (IOException e) {
				e.printStackTrace();
				Log.getLogger().info("Exception " + e.toString());
			}
    	}
		
		FileOutputStream out;
    	try {
    		out = new FileOutputStream(file, true);
    		try {
				out.write(html.getBytes());
				out.flush();
			} catch (IOException e1) {
				e1.printStackTrace();
				Log.getLogger().info("Exception " + e1.toString());
			}
			
			try {
				out.close();
			} catch (IOException e) {
				e.printStackTrace();
				Log.getLogger().info("Exception " + e.toString());
			}
    		
		} catch (FileNotFoundException e) {
			e.printStackTrace();
			Log.getLogger().info("Exception " + e.toString());
		}
	}
	//http://www.zhihu.com/question/31362103
	public void writeAnswer(String dirName, String url, String baseUrl, String html){
		String[] fields = url.split("[/]");
		if(fields.length < 5)
			return;
		
		String[] baseFields = baseUrl.split("[/]");
		if(baseFields.length < 6)
			return;
		String[] pnum = baseFields[5].split("[?]");
		if(pnum.length < 2)
			return;
		String fileName = dirName + "/" + baseFields[3] + " " + baseFields[4] + " " + pnum[1]
				+ " " + fields[3] + " " + fields[4];
		File file = new File(fileName);
    	if(file.exists()){
    		return;
    	}else{
    		try {
				file.createNewFile();
			} catch (IOException e) {
				e.printStackTrace();
				Log.getLogger().info("Exception " + e.toString());
			}
    	}
		
		FileOutputStream out;
    	try {
    		out = new FileOutputStream(file, true);
    		try {
				out.write(html.getBytes());
				out.flush();
			} catch (IOException e1) {
				e1.printStackTrace();
				Log.getLogger().info("Exception " + e1.toString());
			}
			
			try {
				out.close();
			} catch (IOException e) {
				e.printStackTrace();
				Log.getLogger().info("Exception " + e.toString());
			}
    		
		} catch (FileNotFoundException e) {
			e.printStackTrace();
			Log.getLogger().info("Exception " + e.toString());
		}
	}
	

	public void getAnswerPage(String dirName, String url, String baseUrl) throws NotFindPageException, TooBusyException{
		try {
			Page page = client.getPage(url);
			WebResponse response = page.getWebResponse();
			String html = response.getContentAsString();
			int status = response.getStatusCode();
			switch(status){
			case 200:
				//System.out.println("===== fetch answer " + url + " ===== success!");
				Log.getLogger().info("===== fetch answer " + url + " ===== success!");
				break;
			case 404:
				//System.out.println("===== fetch answer " + url + " ===== not found!");
				Log.getLogger().info("===== fetch answer " + url + " ===== not found!");
				throw new NotFindPageException();
			default:
				//System.out.println("===== fetch answer " + url + " ===== too busy!");
				Log.getLogger().info("===== fetch answer " + url + " ===== too busy!");
				throw new TooBusyException(url);
			}
			writeAnswer(dirName, url, baseUrl, html);
		} catch (FailingHttpStatusCodeException e) {
			e.printStackTrace();
			Log.getLogger().info("Exception " + e.toString());
		} catch (MalformedURLException e) {
			e.printStackTrace();
			Log.getLogger().info("Exception " + e.toString());
		} catch (IOException e) {
			e.printStackTrace();
			Log.getLogger().info("Exception " + e.toString());
		}
		
		
	}
	
	
	public void getPage(String url) throws NotFindPageException, TooBusyException{
		
		try {
			Page page = client.getPage(url);
			WebResponse response = page.getWebResponse();
			String html = response.getContentAsString();
			int status = response.getStatusCode();
			switch(status){
			case 200:
				//System.out.println("===== fetch question " + url + " ===== success!");
				Log.getLogger().info("===== fetch topic " + url + " ===== success!");
				break;
			case 404:
				//System.out.println("===== fetch question " + url + " ===== not found!");
				Log.getLogger().info("===== fetch topic " + url + " ===== not found!");
				throw new NotFindPageException();
			default:
				//System.out.println("===== fetch question " + url + " ===== too busy!");
				Log.getLogger().info("===== fetch topic " + url + " ===== too busy!");
				throw new TooBusyException(url);
			}
			
			writeQuestion(dirName, url, html);
			
			Document doc = Jsoup.parse(html);
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
				String subtopicLink = "";
				if(subtopics.size() > 0){
					subtopicName = subtopics.get(0).text();
					subtopicLink = subtopics.get(0).attr("href");
					Log.getLogger().info("===== htmlPage topicName  :" + subtopicName);
					Log.getLogger().info("===== htmlPage topicLink  :" + subtopicLink);
					if(!topicMap.containsKey(subtopicLink)){
						Log.getLogger().info("===== topicMap topicName  :" + topicName + "/" + subtopicName);
						topicMap.put(subtopicLink, topicName + "/" + subtopicName);
						try {
							topicQueue.put(subtopicLink);
						} catch (InterruptedException e) {
							e.printStackTrace();
							Log.getLogger().info("Exception " + e.toString());
						}
					}
				}
				
				if(questionLink.length() > 0){
					
					String answerUrl = prefix + questionLink;		
					int retryNum = 10;
					while(retryNum-- > 0){
						try {
							getAnswerPage(dirName, answerUrl, url);
							break;
						} catch (NotFindPageException e) {
							e.printStackTrace();
							Log.getLogger().info("Exception " + e.toString());
							break;
						} catch (TooBusyException e) {
							e.printStackTrace();
							Log.getLogger().info("Exception " + e.toString());
							try {
								TimeUnit.SECONDS.sleep(1);
							} catch (InterruptedException e1) {
								e1.printStackTrace();
								Log.getLogger().info("Exception " + e1.toString());
							}
						}
					}
					
				}
				
			}
			
			
		} catch (FailingHttpStatusCodeException e) {
			e.printStackTrace();
			Log.getLogger().info("Exception " + e.toString());
		} catch (MalformedURLException e) {
			e.printStackTrace();
			Log.getLogger().info("Exception " + e.toString());
		} catch (IOException e) {
			e.printStackTrace();
			Log.getLogger().info("Exception " + e.toString());
		}
		
	}
	
	public void run(){
		String url = prefix + topicLink + suffix + curPage;
		int retryNum = 10;
		while(retryNum-- > 0){		
			try {
				getPage(url);
				return;
			} catch (NotFindPageException e) {
				e.printStackTrace();
				Log.getLogger().info("Exception " + e.toString());
				return;
			} catch (TooBusyException e) {
				e.printStackTrace();
				Log.getLogger().info("Exception " + e.toString());
				try {
					TimeUnit.SECONDS.sleep(1);
				} catch (InterruptedException e1) {
					e1.printStackTrace();
					Log.getLogger().info("Exception " + e1.toString());
				}
			}
		}
	}
}
