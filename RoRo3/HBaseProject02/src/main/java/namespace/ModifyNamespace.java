package namespace;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.NamespaceDescriptor;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;

import java.io.IOException;

/**
 * 修改命名空间示例
 * 
 * 优化点：
 * 1. 使用 try-with-resources 自动关闭 Admin
 */
public class ModifyNamespace {
    public static void main(String[] args) {
        Connection conn = HBaseConnect.getConnection();

        try (Admin admin = conn.getAdmin()) {
            NamespaceDescriptor employee = admin.getNamespaceDescriptor("employee");
            employee.setConfiguration("date", "2025-10-29");
            employee.setConfiguration("user", "lml");
            employee.removeConfiguration("describe");
            admin.modifyNamespace(employee);
            System.out.println("命名空间修改成功");
        } catch (IOException e) {
            System.err.println("修改命名空间失败: " + e.getMessage());
            e.printStackTrace();
        } finally {
            HBaseConnect.closeConnection();
        }
    }
}
