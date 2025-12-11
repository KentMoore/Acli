package namespace;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.NamespaceDescriptor;

import java.io.IOException;
import java.util.Map;

/**
 * 获取命名空间描述信息
 * 
 * 优化点：
 * 1. 使用 try-with-resources 自动关闭 Admin
 * 2. 使用增强 for 循环
 */
public class GetNamespaceDesc {
    public static void main(String[] args) {
        Connection conn = HBaseConnect.getConnection();

        try (Admin admin = conn.getAdmin()) {
            NamespaceDescriptor employee = admin.getNamespaceDescriptor("commodity1");
            Map<String, String> configuration = employee.getConfiguration();

            System.out.println("命名空间 commodity1 的属性：");
            for (Map.Entry<String, String> entry : configuration.entrySet()) {
                System.out.println("属性：" + entry.getKey() + "\t属性值：" + entry.getValue());
            }
        } catch (IOException e) {
            System.err.println("获取命名空间描述失败: " + e.getMessage());
            e.printStackTrace();
        } finally {
            HBaseConnect.closeConnection();
        }
    }
}
