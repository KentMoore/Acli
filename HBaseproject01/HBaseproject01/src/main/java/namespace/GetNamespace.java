package namespace;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.NamespaceDescriptor;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;

import java.io.IOException;

public class GetNamespace {
    public static void main(String[] args) throws IOException {
        //1.获取连接
        Connection connection= HBaseConnect.getConnection();
        //2.获取Admin对象
        Admin admin=connection.getAdmin();
        //3.调用listNamespaceDescriptors方法获取namespace列表
        NamespaceDescriptor[] namespaceList= admin.listNamespaceDescriptors();//list_namespace
        //4.打印
        for (int i=0;i<namespaceList.length;i++){
            String namespace=namespaceList[i].getName();
            System.out.println(namespace);
        }
        //5.关闭连接
        HBaseConnect.closeConnection();
    }
}
