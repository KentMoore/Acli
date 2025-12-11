package table;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;

import java.io.IOException;

/**
 * 获取所有表列表
 * 
 * 优化点：
 * 1. 完善功能实现
 * 2. 使用 try-with-resources 自动关闭 Admin
 */
public class GetTablelist {
    public static void main(String[] args) {
        Connection conn = HBaseConnect.getConnection();

        try (Admin admin = conn.getAdmin()) {
            TableName[] tableNames = admin.listTableNames();
            System.out.println("HBase 中的所有表：");
            for (TableName tableName : tableNames) {
                System.out.println("  - " + tableName.getNameAsString());
            }
            System.out.println("共 " + tableNames.length + " 张表");
        } catch (IOException e) {
            System.err.println("获取表列表失败: " + e.getMessage());
            e.printStackTrace();
        } finally {
            HBaseConnect.closeConnection();
        }
    }
}
