package test;

import java.util.concurrent.RejectedExecutionException;
import java.util.concurrent.Semaphore;
import java.util.concurrent.ThreadPoolExecutor;

public class BoundedExecutor {
	private final ThreadPoolExecutor exec;
	private final Semaphore sem;
	
	public BoundedExecutor(ThreadPoolExecutor exec, int bound){
		this.exec = exec;
		this.sem = new Semaphore(bound);
	}
	
	public void execute(final Runnable cmd) throws InterruptedException, RejectedExecutionException{
		sem.acquire();
		try{
			exec.execute(new Runnable(){
				public void run(){
					try{
						cmd.run();
					}finally{
						sem.release();
					}
				}
			});
		}catch(RejectedExecutionException e){
			sem.release();
			throw e;
		}
		
	}
	
	public boolean isShutdown(){
		return this.exec.isShutdown();
	}
	
	public void shutdown(){
		this.exec.shutdown();
	}
}
