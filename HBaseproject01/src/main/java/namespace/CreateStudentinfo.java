package namespace;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.io.compress.Compression;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;

public class CreateStudentinfo {
    public static void main(String[] args) throws IOException {
        // 获取连接
        Connection connection = HBaseConnect.getConnection();
        Admin admin = connection.getAdmin();

        // 表名：命名空间 commodity1 下的 fruit_table
        TableName table = TableName.valueOf("commodity1:fruit_table");

        // 如果表已经存在，先删除再重建（小实验用，生产别这么干）
        if (admin.tableExists(table)) {
            System.out.println("Table exists. Deleting and recreating...");
            admin.disableTable(table);
            admin.deleteTable(table);
        }

        // 列族：fruit_info（水果基础信息）
        ColumnFamilyDescriptor fruitInfoCF = ColumnFamilyDescriptorBuilder
                .newBuilder(Bytes.toBytes("fruit_info"))
                .setMaxVersions(3)
                .setCompressionType(Compression.Algorithm.SNAPPY) // 集群有 Snappy 再用
                .build();

        // 列族：sale_info（销售相关信息）
        ColumnFamilyDescriptor saleInfoCF = ColumnFamilyDescriptorBuilder
                .newBuilder(Bytes.toBytes("sale_info"))
                .setMaxVersions(3)
                .build();

        // 表描述符
        TableDescriptor tableDescriptor = TableDescriptorBuilder.newBuilder(table)
                .setReadOnly(false)
                .setColumnFamily(fruitInfoCF)
                .setColumnFamily(saleInfoCF)
                .build();

        // 预分 3 个 region
        byte[][] splits = {Bytes.toBytes("key100"), Bytes.toBytes("key500")};
        admin.createTable(tableDescriptor, splits);

        System.out.println("Table created: commodity1:fruit_table with CFs: fruit_info, sale_info");

        // 关闭资源
        admin.close();
        HBaseConnect.closeConnection();
    }
}