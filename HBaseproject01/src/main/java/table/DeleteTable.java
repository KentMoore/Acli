package table;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;

import java.io.IOException;

/**
 * 删除表示例
 * 
 * 优化点：
 * 1. 添加表存在性检查
 * 2. 添加表启用状态检查
 * 3. 使用 try-with-resources 自动关闭 Admin
 */
public class DeleteTable {
    public static void main(String[] args) {
        Connection conn = HBaseConnect.getConnection();
        TableName tableName = TableName.valueOf("commodity1:fruit_table");

        // 使用 try-with-resources 自动关闭 Admin
        try (Admin admin = conn.getAdmin()) {

            // 检查表是否存在
            if (!admin.tableExists(tableName)) {
                System.out.println("表 " + tableName + " 不存在，无需删除");
                return;
            }

            // 如果表已启用，先禁用
            if (admin.isTableEnabled(tableName)) {
                System.out.println("正在禁用表 " + tableName + "...");
                admin.disableTable(tableName);
            }

            // 删除表
            admin.deleteTable(tableName);
            System.out.println("表 " + tableName + " 已成功删除");

        } catch (IOException e) {
            System.err.println("删除表失败: " + e.getMessage());
            e.printStackTrace();
        } finally {
            HBaseConnect.closeConnection();
        }
    }
}
