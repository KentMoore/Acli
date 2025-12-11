package namespace;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.NamespaceDescriptor;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Admin;

import java.io.IOException;

/**
 * 获取所有命名空间列表
 * 
 * 优化点：
 * 1. 使用 try-with-resources 自动关闭 Admin
 */
public class GetNamespace {
    public static void main(String[] args) {
        Connection connection = HBaseConnect.getConnection();

        try (Admin admin = connection.getAdmin()) {
            NamespaceDescriptor[] namespaceList = admin.listNamespaceDescriptors();
            System.out.println("HBase 中所有的 namespace：");
            System.out.println("---------------------------");
            for (NamespaceDescriptor namespace : namespaceList) {
                System.out.println(namespace.getName());
            }
            System.out.println("---------------------------");
        } catch (IOException e) {
            System.err.println("获取命名空间列表失败: " + e.getMessage());
            e.printStackTrace();
        } finally {
            HBaseConnect.closeConnection();
        }
    }
}
