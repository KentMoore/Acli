package table;
//在employee命名空间内创建staff_info表，
//通过表的自定义属性"comment",添加表的描述信息"Employee information sheet"，
//预分区数组为[“key10”,”key20”]
//设置列族development_info，设置列族最大版本数为3，列族数据缓存到内存，
//设置列族sale_info，每个数据块的大小为64kB，数据压缩方式设置为“SNAPPY”

import connect.HBaseConnect;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.io.compress.Compression;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;

public class CreateTable3 {
    public static void main(String[] args) throws IOException {
        //1.获取HBase连接
        Connection conn= HBaseConnect.getConnection();
        //2.获取Admin对象
        Admin admin= conn.getAdmin();
        //构造列族对象
        ColumnFamilyDescriptor development_info= ColumnFamilyDescriptorBuilder
                .newBuilder("development_info".getBytes())
                .setMaxVersions(3)
                .setInMemory(true)
                .build();
        ColumnFamilyDescriptor sale_info=ColumnFamilyDescriptorBuilder
                .newBuilder("sale_info".getBytes())
                .setBlocksize(64*1024)
                .build();
        //构造表对象
        TableName tableName=TableName.valueOf("employee:staff1");
        TableDescriptor staff_info=TableDescriptorBuilder
                .newBuilder(tableName)
                .setColumnFamily(development_info)
                .setColumnFamily(sale_info)
                .setValue("comment","employee staff information")
                .build();
        //建表
        if(admin.tableExists(tableName)){
            System.out.println("表已存在，不可重复创建");
        }else{
            admin.createTable(staff_info);
            System.out.println("表已成功创建");
        }
        HBaseConnect.closeConnection();
    }
}
