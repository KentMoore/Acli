package namespace;

import org.apache.hadoop.hbase.NamespaceDescriptor;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;

import connect.HBaseConnect;

import java.io.IOException;

public class CreateNamespace4 {
    public static void main(String[] args) throws IOException {
        Connection connect = HBaseConnect.getConnection();
        Admin admin = connect.getAdmin();
        NamespaceDescriptor namespaceDescriptor = NamespaceDescriptor
                .create("commodity")
                .addConfiguration("describe", "record commodity information")
                .build();
        admin.createNamespace(namespaceDescriptor);
        HBaseConnect.closeConnection();
    }
}