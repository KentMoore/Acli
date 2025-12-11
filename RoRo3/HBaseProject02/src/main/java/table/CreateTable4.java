package table;

import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.*;
import connect.HBaseConnect;

import java.io.IOException;

public class CreateTable4 {
    public static void main(String[] args) throws IOException {
        // 1.获取HBase连接
        Connection conn = HBaseConnect.getConnection();
        // 2.获取Admin对象
        Admin admin = conn.getAdmin();
        // 3.创建表
        // 3.1构造列族对象
        String dd = "fruit_info";
        String ss = "sale_info";
        ColumnFamilyDescriptor df = ColumnFamilyDescriptorBuilder
                .newBuilder(dd.getBytes()) // 列族名
                .setMaxVersions(3) // 设置最大版本数为3
                .setInMemory(true) // 列族数据缓存在内存
                .build();
        ColumnFamilyDescriptor sf = ColumnFamilyDescriptorBuilder
                .newBuilder(ss.getBytes()) // 列族名
                .setMaxVersions(3) // 设置最大版本数为3
                .setInMemory(true) // 列族数据缓存在内存
                .build();
        // 3.2构造表对象
        TableName test1Name = TableName.valueOf("commodity:fruit_table"); // 使用Table构造表名test1
        TableDescriptor test1 = TableDescriptorBuilder
                .newBuilder(test1Name) // 表名
                .setColumnFamily(df) // 添加列族到表对象
                .setColumnFamily(sf)
                .build();
        // 3.3admin建表
        if (!admin.tableExists(test1Name)) {
            admin.createTable(test1);
        } else {
            System.out.println("表已存在，不可创建");
        }
        // 4.关闭连接
        HBaseConnect.closeConnection();
    }
}