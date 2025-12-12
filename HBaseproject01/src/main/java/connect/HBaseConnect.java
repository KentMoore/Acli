package connect;

import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.client.ConnectionFactory;

import java.io.IOException;

/**
 * HBase 连接工具类 - 单例模式
 * 
 * 优化点：
 * 1. 使用双重检查锁定的单例模式，确保全局只有一个连接实例
 * 2. 修复了原 closeConnection() 方法的 Bug（原方法每次调用都创建新连接）
 * 3. 使用 volatile 保证多线程可见性
 */
public class HBaseConnect {

    // 使用 volatile 保证多线程环境下的可见性
    private static volatile Connection connection = null;

    // 私有化构造函数，防止外部实例化
    private HBaseConnect() {
    }

    /**
     * 获取 HBase 连接（单例模式）
     * 使用双重检查锁定确保线程安全
     */
    public static Connection getConnection() {
        if (connection == null || connection.isClosed()) {
            synchronized (HBaseConnect.class) {
                try {
                    if (connection == null || connection.isClosed()) {
                        // 1、创建配置对象
                        Configuration configuration = HBaseConfiguration.create();
                        // 2、添加配置信息
                        // 2.1、Hmaster
                        configuration.set("hbase.master", "master");
                        // 2.2、Zookeeper集群
                        configuration.set("hbase.zookeeper.quorum", "master:2181,worker1:2181,worker2:2181");
                        // 3、创建连接
                        connection = ConnectionFactory.createConnection(configuration);
                        System.out.println("HBase 连接已创建");
                    }
                } catch (IOException e) {
                    System.err.println("创建 HBase 连接失败: " + e.getMessage());
                    e.printStackTrace();
                }
            }
        }
        return connection;
    }

    /**
     * 关闭 HBase 连接
     * 修复：现在正确关闭已有的连接实例，而不是创建新连接
     */
    public static void closeConnection() {
        synchronized (HBaseConnect.class) {
            try {
                if (connection != null && !connection.isClosed()) {
                    System.out.println("HBase 关闭连接");
                    connection.close();
                    connection = null;
                }
            } catch (IOException e) {
                System.err.println("关闭 HBase 连接失败: " + e.getMessage());
                e.printStackTrace();
            }
        }
    }

    /**
     * 检查连接是否有效
     */
    public static boolean isConnectionValid() {
        return connection != null && !connection.isClosed();
    }
}
