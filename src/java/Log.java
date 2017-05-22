package test;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Calendar;

import org.apache.log4j.FileAppender;
import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.apache.log4j.SimpleLayout;

public final class Log {

	private final static Logger logger = Logger.getLogger(Log.class);
	
	static{
		SimpleLayout layout = new SimpleLayout();
		FileAppender appender = null;
		
		try {
			String timestamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(Calendar.getInstance().getTime());
			String fileName = "./log/" + timestamp + ".log";
			appender = new FileAppender(layout, fileName, false);
		} catch (IOException e) {
			e.printStackTrace();
		}
		logger.addAppender(appender);
		logger.setLevel(Level.INFO);
	}
	
	public static Logger getLogger(){
		return logger;
	}
}
