package namespace;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;

import java.io.IOException;

/**
 * 删除命名空间示例
 * 
 * 优化点：
 * 1. 使用 try-with-resources 自动关闭 Admin
 */
public class DeleteNamespace {
    public static void main(String[] args) {
        Connection conn = HBaseConnect.getConnection();
        String namespaceName = "employee7";

        try (Admin admin = conn.getAdmin()) {
            admin.deleteNamespace(namespaceName);
            System.out.println("命名空间 " + namespaceName + " 已删除");
        } catch (IOException e) {
            System.err.println("删除命名空间失败: " + e.getMessage());
            e.printStackTrace();
        } finally {
            HBaseConnect.closeConnection();
        }
    }
}
