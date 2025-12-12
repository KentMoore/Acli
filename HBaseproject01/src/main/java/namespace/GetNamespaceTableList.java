package namespace;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;
import java.io.IOException;

public class GetNamespaceTableList {
    public static void main(String[] args) throws IOException {
        Connection connect = HBaseConnect.getConnection();
        Admin admin = connect.getAdmin();
        TableName[] tableList = admin.listTableNamesByNamespace("school1");
        System.out.println("命名空间school1中的表有：");
        for (int i = 0; i < tableList.length; i++) {

            System.out.println(tableList[i].getNameAsString());
        }
        HBaseConnect.closeConnection();
    }
}
