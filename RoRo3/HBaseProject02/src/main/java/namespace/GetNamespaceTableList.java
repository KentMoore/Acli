package namespace;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;

import java.io.IOException;

/**
 * 获取命名空间下的表列表
 * 
 * 优化点：
 * 1. 移除未使用的 import
 * 2. 使用 try-with-resources 自动关闭 Admin
 */
public class GetNamespaceTableList {
    public static void main(String[] args) {
        Connection connect = HBaseConnect.getConnection();

        try (Admin admin = connect.getAdmin()) {
            TableName[] tableList = admin.listTableNamesByNamespace("school1");
            System.out.println("命名空间 school1 中的表有：");
            for (TableName tableName : tableList) {
                System.out.println("  - " + tableName.getNameAsString());
            }
        } catch (IOException e) {
            System.err.println("获取表列表失败: " + e.getMessage());
            e.printStackTrace();
        } finally {
            HBaseConnect.closeConnection();
        }
    }
}
