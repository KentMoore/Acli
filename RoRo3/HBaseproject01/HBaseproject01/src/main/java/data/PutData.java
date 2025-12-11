package data;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;

public class PutData {
    public static void main(String[] args) throws IOException {
        //1.获取连接
        Connection connection= HBaseConnect.getConnection();
        //2.获取表对象
        TableName tableName=TableName.valueOf("employee:staff_info");
        Table table=connection.getTable(tableName);
        //3.实例化Put对象，传入rowkey    staff001, development_info staff_name:zhangsan,staff_age:26,
        // staff_phone:17664487906
        Put put=new Put(Bytes.toBytes("staff001"));
        //4.构造put,将数据填入put对象中
        //put "employee:staff1","staff001","development_info","staff_name","zhangsan"
        Put put1=put.addColumn(
                Bytes.toBytes("development_info"),
                Bytes.toBytes("staff_name"),
                System.currentTimeMillis(),
                Bytes.toBytes("zhangsan")
        );
        Put put2=put.addColumn(
                Bytes.toBytes("development_info"),
                Bytes.toBytes("staff_age"),
                System.currentTimeMillis(),
                Bytes.toBytes("26")
        );
        Put put3=put.addColumn(
                Bytes.toBytes("development_info"),
                Bytes.toBytes("staff_phone"),
                System.currentTimeMillis(),
                Bytes.toBytes("17664487906")
        );
        Put put4=put.addColumn(
                Bytes.toBytes("sale_info"),
                Bytes.toBytes("staff_name"),
                System.currentTimeMillis(),
                Bytes.toBytes("wangwu")
        );
        Put put5=put.addColumn(
                Bytes.toBytes("sale_info"),
                Bytes.toBytes("staff_age"),
                System.currentTimeMillis(),
                Bytes.toBytes("23")
        );
        Put put6=put.addColumn(
                Bytes.toBytes("sale_info"),
                Bytes.toBytes("staff_phone"),
                System.currentTimeMillis(),
                Bytes.toBytes("17880657921")
        );
        table.put(put1);
        table.put(put2);
        table.put(put3);
        table.put(put4);
        table.put(put5);
        table.put(put6);
        HBaseConnect.closeConnection();

    }
}
