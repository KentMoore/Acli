package namespace;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.NamespaceDescriptor;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;

import java.io.IOException;

/**
 * 创建命名空间示例
 * 
 * 优化点：
 * 1. 使用 try-with-resources 自动关闭 Admin
 */
public class CreateNamespace {
    public static void main(String[] args) {
        Connection conn = HBaseConnect.getConnection();

        try (Admin admin = conn.getAdmin()) {
            NamespaceDescriptor namespace = NamespaceDescriptor
                    .create("commodity1")
                    .addConfiguration("user", "root")
                    .addConfiguration("describe", "fstp data")
                    .build();
            admin.createNamespace(namespace);
            System.out.println("命名空间创建成功");
        } catch (IOException e) {
            System.err.println("创建命名空间失败: " + e.getMessage());
            e.printStackTrace();
        } finally {
            HBaseConnect.closeConnection();
        }
    }
}
