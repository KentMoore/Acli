package table;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.*;

import java.io.IOException;

public class ModifyTable {
    public static void main(String[] args) throws IOException {
        //1.获取HBase连接
        Connection conn= HBaseConnect.getConnection();
        //2.获取Admin对象
        Admin admin= conn.getAdmin();
        //3.获取要修改的表对象
        TableName tableName=TableName.valueOf("employee:staff_info");
        TableDescriptor staff_info=admin.getDescriptor(tableName);
        //4.获取要修改的列族对象
        ColumnFamilyDescriptor sale_info=staff_info.getColumnFamily("sale_info".getBytes());
        //5.修改列族对象
        ColumnFamilyDescriptor modify_sale_info= ColumnFamilyDescriptorBuilder
                .newBuilder(sale_info)
                .setMaxVersions(1)
                .setTimeToLive(3600)
                .build();
        //6.新增列族，首先要构造列族对象
        ColumnFamilyDescriptor finance_info=ColumnFamilyDescriptorBuilder
                .newBuilder("finance_info".getBytes())
                .setInMemory(true)
                .build();
        //7.修改表对象
        TableDescriptor modify_staff_info=TableDescriptorBuilder
                .newBuilder(staff_info)
                .modifyColumnFamily(modify_sale_info)    //修改列族
                .setColumnFamily(finance_info)           //添加列族
                .removeColumnFamily("development_info".getBytes())   //删除列族
                .setValue("comment","new employee information sheet")
                .setValue("user","root")
                .setValue("createTime","2025-11-07")
                .removeValue("user".getBytes())
                .build();
        //8.admin调用modifyTable方法修改表
        admin.modifyTable(modify_staff_info);
        //9.关闭连接
        HBaseConnect.closeConnection();
    }
}
