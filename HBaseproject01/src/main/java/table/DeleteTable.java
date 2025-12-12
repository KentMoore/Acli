package table;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;

import java.io.IOException;

public class DeleteTable {
    public static void main(String[] args) throws IOException {
        //1.获取HBase连接
        Connection conn= HBaseConnect.getConnection();
        //2.获取Admin对象
        Admin admin= conn.getAdmin();
        TableName tableName=TableName.valueOf("employee:staff_info");
        //3.停用表
        admin.disableTable(tableName);
        //4.删除表
        admin.deleteTable(tableName);
        //5.关闭连接
        HBaseConnect.closeConnection();
    }
}
