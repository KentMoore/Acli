package namespace;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;

import java.io.IOException;

public class DeleteNamespace {
    public static void main(String[] args) throws IOException {
        Connection conn= HBaseConnect.getConnection();
        Admin admin= conn.getAdmin();
        admin.deleteNamespace("employee");
        HBaseConnect.closeConnection();
    }
}
