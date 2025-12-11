package table;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;

import java.io.IOException;

public class GetTableList {
    public static void main(String[] args) throws IOException {
        //1.获取HBase连接
        Connection conn= HBaseConnect.getConnection();
        //2.获取Admin对象
        Admin admin= conn.getAdmin();
        TableName[] tableNameList=admin.listTableNames();
        for(int i=0;i<tableNameList.length;i++){
            System.out.println(tableNameList[i].getNameAsString());
        }
    }
}
