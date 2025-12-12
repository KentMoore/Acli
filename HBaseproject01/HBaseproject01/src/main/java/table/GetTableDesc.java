package table;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.TableDescriptor;

import java.io.IOException;

public class GetTableDesc {
    public static void main(String[] args) throws IOException {
        //1.获取HBase连接
        Connection conn= HBaseConnect.getConnection();
        //2.获取Admin对象
        Admin admin= conn.getAdmin();
        TableDescriptor tableDescriptor=admin.getDescriptor(TableName.valueOf("commodity1:fruit_info"));
        System.out.println(tableDescriptor);
        HBaseConnect.closeConnection();
    }
}
