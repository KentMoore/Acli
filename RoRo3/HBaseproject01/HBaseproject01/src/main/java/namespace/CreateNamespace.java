package namespace;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.NamespaceDescriptor;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;

import java.io.IOException;

public class CreateNamespace {
    public static void main(String[] args) throws IOException {
        //1.获取HBase连接
        Connection conn= HBaseConnect.getConnection();
        //2.获取Admin对象
        Admin admin= conn.getAdmin();
        //3.创建命名空间
        //3.1构造一个命名空间对象
        NamespaceDescriptor namespace= NamespaceDescriptor
                .create("commodity1")
                .addConfiguration("user","root")
                .addConfiguration("describe","empolyee data")
                .build();
        //3.2admin调用createNamespace方法创建命名空间
        admin.createNamespace(namespace);
        //4.关闭连接
        HBaseConnect.closeConnection();
    }
}
