package table;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.io.compress.Compression;

import java.io.IOException;

/**
 * 修改表结构示例
 * 
 * 功能：
 * 1. 修改已有列族的属性（如 maxVersions、TTL）
 * 2. 添加新的列族
 * 3. 修改表级属性
 * 
 * 优化点：
 * 1. 使用 try-with-resources 自动关闭 Admin
 * 2. 添加表存在性检查
 * 3. 修复原代码的语法错误
 */
public class ModifyTable {
    public static void main(String[] args) {
        Connection conn = HBaseConnect.getConnection();
        TableName tableName = TableName.valueOf("employee:staff_info");

        try (Admin admin = conn.getAdmin()) {
            // 1. 检查表是否存在
            if (!admin.tableExists(tableName)) {
                System.out.println("表 " + tableName + " 不存在，无法修改");
                return;
            }

            // 2. 获取当前表描述符
            TableDescriptor currentDescriptor = admin.getDescriptor(tableName);
            System.out.println("正在修改表 " + tableName + "...");

            // 3. 获取并修改已有的列族 (sale_info)
            ColumnFamilyDescriptor saleInfoCF = currentDescriptor.getColumnFamily("sale_info".getBytes());
            ColumnFamilyDescriptor modifiedSaleInfo = null;
            if (saleInfoCF != null) {
                modifiedSaleInfo = ColumnFamilyDescriptorBuilder
                        .newBuilder(saleInfoCF)
                        .setMaxVersions(1)
                        .setTimeToLive(3600) // 1小时过期
                        .build();
            }

            // 4. 创建新的列族 (finance_info)
            ColumnFamilyDescriptor financeInfoCF = ColumnFamilyDescriptorBuilder
                    .newBuilder("finance_info".getBytes())
                    .setInMemory(true)
                    .setCompressionType(Compression.Algorithm.SNAPPY)
                    .build();

            // 5. 构建新的表描述符
            TableDescriptorBuilder builder = TableDescriptorBuilder.newBuilder(currentDescriptor);

            // 修改已有列族
            if (modifiedSaleInfo != null) {
                builder.modifyColumnFamily(modifiedSaleInfo);
            }

            // 添加新列族（如果不存在）
            if (currentDescriptor.getColumnFamily("finance_info".getBytes()) == null) {
                builder.setColumnFamily(financeInfoCF);
            }

            // 修改表级属性
            builder.setValue("comment", "new employee information sheet")
                    .setValue("createTime", "2025-12-06");

            TableDescriptor modifiedDescriptor = builder.build();

            // 6. 应用修改
            admin.modifyTable(modifiedDescriptor);
            System.out.println("表 " + tableName + " 修改成功");

            // 7. 打印修改后的表信息
            TableDescriptor newDescriptor = admin.getDescriptor(tableName);
            System.out.println("修改后的列族列表：");
            for (ColumnFamilyDescriptor cf : newDescriptor.getColumnFamilies()) {
                System.out.println("  - " + cf.getNameAsString() +
                        " (maxVersions=" + cf.getMaxVersions() +
                        ", TTL=" + cf.getTimeToLive() + "s)");
            }

        } catch (IOException e) {
            System.err.println("修改表失败: " + e.getMessage());
            e.printStackTrace();
        } finally {
            HBaseConnect.closeConnection();
        }
    }
}
