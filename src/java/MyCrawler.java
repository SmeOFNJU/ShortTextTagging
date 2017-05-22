package test;

import java.io.File;
import java.io.IOException;
import java.net.MalformedURLException;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

import com.gargoylesoftware.htmlunit.FailingHttpStatusCodeException;
import com.gargoylesoftware.htmlunit.WebClient;
import com.gargoylesoftware.htmlunit.WebResponse;
import com.gargoylesoftware.htmlunit.html.HtmlPage;

public class MyCrawler {

	private int pageNum =-1;
	private int curPage = 1;
	private BlockingQueue<String> topicQueue = new LinkedBlockingQueue<String>();//new ArrayBlockingQueue<String>(500);
	private ConcurrentHashMap<String, String> topicMap = new ConcurrentHashMap<String, String>();
	
	//private ThreadPoolExecutor executor = 
	//new ArrayBlockingQueue<Runnable>(1000)
	private final String prefix = "http://www.zhihu.com";
	private final String suffix = "/questions?page=";
	
	private BoundedExecutor executor = new BoundedExecutor(new ThreadPoolExecutor(5, 10, 200, TimeUnit.SECONDS, 
			new LinkedBlockingQueue<Runnable>()), 5000);
	
	public WebClient create(){
		WebClient client = new WebClient();
		client.getOptions().setJavaScriptEnabled(false);
		client.getOptions().setCssEnabled(false);
		client.getOptions().setThrowExceptionOnFailingStatusCode(false);
		return client;
	}
	
	public int getPageNum(WebClient client, String url) throws NotFindPageException, TooBusyException{
		int num = 1;
		try {
			HtmlPage page = client.getPage(url);
			WebResponse response = page.getWebResponse();
			String html = response.getContentAsString();
			int status = response.getStatusCode();
			switch(status){
			case 200:
				Log.getLogger().info("===== fetch page num " + url + " ===== success!");
				break;
			case 404:
				Log.getLogger().info("===== fetch page num " + url + " ===== not found!");
				throw new NotFindPageException();
			default:
				Log.getLogger().info("===== fetch page num " + url + " ===== too busy!");
				throw new TooBusyException(url);
			}
			
			Document doc = Jsoup.parse(html);

			Elements pages = doc.select("div[class=zm-invite-pager]");
			if(pages.size() > 0){
				Elements pageNums = pages.get(0).select("a");
				if(pageNums.size() > 2){
					num = Integer.parseInt(pageNums.get(pageNums.size() - 2).text());
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
		
		return num;
	}
	
	public void dispatcher() throws InterruptedException{
		WebClient client = create();
		while(true){
			try {
				String topicLink = "";
				topicLink = topicQueue.take();				
				curPage = 1;
				String url = prefix + topicLink + suffix + curPage;
				int retryNum = 10;
				while(retryNum-- > 0){
					try {
						pageNum = getPageNum(client, url);				
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
				curPage = 1;
				String topicName = topicMap.get(topicLink);
				Log.getLogger().info("===== topicQueue topicName  :" + topicName);
				Log.getLogger().info("===== " + topicName + " page number :" + pageNum);
				if(topicName == null)
					continue;
				String dirName = "./data/" + topicName;
				File dir = new File(dirName);
				if(!dir.exists()){
					dir.mkdirs();
				}
				while(curPage <= pageNum){
					if(!executor.isShutdown()){
						executor.execute(new Worker(curPage, topicLink, topicQueue, topicMap, topicName));
						curPage++;
					}else{
						Log.getLogger().info("Exception exector have been shutdown");
					}
				
				}
				
				
			} catch (InterruptedException e) {
				e.printStackTrace();
				Log.getLogger().info("Exception " + e.toString());
				throw new InterruptedException();
			}
		}

	}
	
	public void stop(){
		executor.shutdown();
		Log.getLogger().info("===== over =====");
	}
	
	public void start(){	
		//topicMap.put("/topic/19584724", "��Ʒ");
		//topicQueue.add("/topic/19584724");
		//topicMap.put("/topic/19553622", "����");
		//topicQueue.add("/topic/19553622");
		
		//topicMap.put("/topic/20013723", "��������");
		//topicQueue.add("/topic/20013723");
		//topicMap.put("/topic/19551469", "����");
		//topicQueue.add("/topic/19551469");
		topicMap.put("/topic/19551915", "����");
		topicQueue.add("/topic/19551915");
		
		try {
			dispatcher();
		} catch (InterruptedException e) {
			stop();
			e.printStackTrace();
			Log.getLogger().info("Exception " + e.toString());
		}

		
	}
	
	public static void main(String []args){
		MyCrawler crawler = new MyCrawler();
		long begin = System.currentTimeMillis();
		crawler.start();
		long end = System.currentTimeMillis();
		Log.getLogger().info("cost time : " + (end - begin)/1000.0);
	}
}



/*
����   /topic/19554827

����  /topic/19551469

�ڽ� /topic/19570783

���� /topic/19551424

���� /topic/19550874

��Ӱ /topic/19550429

���� /topic/19550453

��ʷ /topic/19551077

��ͨ /topic/19557401

��ѧ /topic/19556423

��Ϸ /topic/19550994

���� /topic/19588006

�鼮 /topic/19553713

ʳ�� /topic/19552062

���� /topic/19553622

���� /topic/19812101

��Ʒ /topic/19584724

��ͥ /topic/19556074
*/


/*
 * ������
 * ���ʽ
 * ����
 * ְҵ��չ
 * ����
 * �Ƽ�
 * 
 * */


/*
 * ����
 * ���� /topic/19551915
 * ���
 * ��ҵ
 * ����
 * 
 * 
 * 
 * 
 * */






