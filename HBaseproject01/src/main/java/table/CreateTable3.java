package table;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.io.compress.Compression;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;

/**
 * 创建表示例（带预分区）
 * 
 * 优化点：
 * 1. 修复逻辑 Bug：原代码表存在判断反了
 * 2. 使用两个列族
 * 3. 使用 try-with-resources 自动关闭 Admin
 */
public class CreateTable3 {
        public static void main(String[] args) {
                Connection conn = HBaseConnect.getConnection();

                try (Admin admin = conn.getAdmin()) {
                        // 构造列族对象
                        ColumnFamilyDescriptor developmentInfo = ColumnFamilyDescriptorBuilder
                                        .newBuilder("development_info".getBytes())
                                        .setMaxVersions(3)
                                        .setInMemory(true)
                                        .build();

                        ColumnFamilyDescriptor saleInfo = ColumnFamilyDescriptorBuilder
                                        .newBuilder("sale_info".getBytes())
                                        .setBlocksize(64 * 1024)
                                        .setCompressionType(Compression.Algorithm.SNAPPY)
                                        .build();

                        // 构造表对象
                        TableName tableName = TableName.valueOf("employee:staff_info");
                        TableDescriptor staffInfo = TableDescriptorBuilder
                                        .newBuilder(tableName)
                                        .setColumnFamily(developmentInfo) // 添加 development_info 列族
                                        .setColumnFamily(saleInfo) // 添加 sale_info 列族
                                        .setValue("comment", "employee staff information")
                                        .build();

                        // 预分区键
                        byte[][] keySplits = new byte[][] {
                                        Bytes.toBytes("key10"),
                                        Bytes.toBytes("key20"),
                        };

                        // 修复：原代码逻辑反了
                        if (!admin.tableExists(tableName)) {
                                admin.createTable(staffInfo, keySplits);
                                System.out.println("表已成功创建");
                        } else {
                                System.out.println("表已存在，不可重复创建");
                        }

                } catch (IOException e) {
                        System.err.println("创建表失败: " + e.getMessage());
                        e.printStackTrace();
                } finally {
                        HBaseConnect.closeConnection();
                }
        }
}
