package namespace;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.NamespaceDescriptor;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;

import java.io.IOException;

public class ModifyNamespace {
    public static void main(String[] args) throws IOException {
        Connection conn= HBaseConnect.getConnection();
        Admin admin= conn.getAdmin();
        NamespaceDescriptor employee=admin.getNamespaceDescriptor("employee");
        //setConfiguration或removeConfiguration去添加或删除属性
        employee.setConfiguration("date","2025-10-29");
        employee.setConfiguration("user","lml");
        employee.removeConfiguration("describe");
        //admin调用modifyNamespace方法修改命名空间
        admin.modifyNamespace(employee);
        HBaseConnect.closeConnection();
    }
}
