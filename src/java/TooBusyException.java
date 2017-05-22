package test;

public class TooBusyException extends Exception{
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private String url;
	
	public TooBusyException(String u){
		url = u;
	}
	public String getUrl(){
		return url;
	}
}
