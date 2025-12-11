package connect;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;

import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.ConnectionFactory;
import java.io.IOException;

public class HBaseConnect {
    public static Connection getConnection(){
       Connection connection=null;
        //1.创建配置对象
        Configuration configuration= HBaseConfiguration.create();
        //2.添加配置信息
        //2.1Hmaster
        configuration.set("hbase.master","master");
        //2.2Zookeeper集群
        configuration.set("hbase.zookeeper.quorum","master:2181,worker1:2181,worker2:2181");
       try{
        //3.创建连接
        connection= ConnectionFactory.createConnection(configuration);
       } catch (IOException e) {
           e.printStackTrace();
       }
       return connection;

    }
    public static void  closeConnection(){
        Connection connection=HBaseConnect.getConnection();
        try {
            if (connection.isClosed() == false) {
                System.out.println("HBase关闭连接");
                connection.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
