package table;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.io.compress.Compression;
import org.apache.hadoop.hbase.regionserver.BloomType;

import java.io.IOException;

/**
 * 创建表示例
 * 
 * 优化点：
 * 1. 使用 try-with-resources 自动关闭 Admin
 */
public class CreateTable {
    public static void main(String[] args) {
        Connection conn = HBaseConnect.getConnection();

        try (Admin admin = conn.getAdmin()) {
            // 构造列族对象
            ColumnFamilyDescriptor df = ColumnFamilyDescriptorBuilder
                    .newBuilder("df".getBytes())
                    .setMaxVersions(3)
                    .setInMemory(true)
                    .setCompressionType(Compression.Algorithm.LZ4)
                    .setBloomFilterType(BloomType.NONE)
                    .build();

            // 构造表对象
            TableName test1Name = TableName.valueOf("commodity1:fruit_table");
            TableDescriptor test1 = TableDescriptorBuilder
                    .newBuilder(test1Name)
                    .setColumnFamily(df)
                    .setReadOnly(true)
                    .build();

            // 创建表
            if (!admin.tableExists(test1Name)) {
                admin.createTable(test1);
                System.out.println("表已创建");
            } else {
                System.out.println("表已存在，不可创建");
            }
        } catch (IOException e) {
            System.err.println("创建表失败: " + e.getMessage());
            e.printStackTrace();
        } finally {
            HBaseConnect.closeConnection();
        }
    }
}
