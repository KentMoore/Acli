package table;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.regionserver.BloomType;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;

public class CreateTable2 {
    public static void main(String[] args) throws IOException {
        //1.获取HBase连接
        Connection conn= HBaseConnect.getConnection();
        //2.获取Admin对象
        Admin admin= conn.getAdmin();
        ColumnFamilyDescriptor sf= ColumnFamilyDescriptorBuilder
                .newBuilder("sf".getBytes())
                .setTimeToLive(3600*24)
                .setMinVersions(1)
                .setBlocksize(32*1024)
                .setBloomFilterType(BloomType.ROW)
                .build();
        TableName test2Name=TableName.valueOf("employee:test2");
        TableDescriptor test2=TableDescriptorBuilder
                .newBuilder(test2Name)
                .setColumnFamily(sf)
                .setValue("comment","test2 imformation")
                .build();
        //定义一个预分区数组
        byte[][] keySplits=new byte[][]{
                Bytes.toBytes("10"),
                Bytes.toBytes("20"),
                Bytes.toBytes("30"),
                Bytes.toBytes("40")
        };
        if(!admin.tableExists(test2Name)){
            admin.createTable(test2,keySplits);//预分区数组在建表时传进来
            System.out.println("表已成功创建");
        }else{
            System.out.println("表已存在，不可重复创建");
        }

        HBaseConnect.closeConnection();
    }
}
