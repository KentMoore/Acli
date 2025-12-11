package data;

import connect.HBaseConnect;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;

/**
 * 单条数据插入示例
 * 
 * 优化点：
 * 1. 移除未使用的 import
 * 2. 使用 try-with-resources 自动关闭 Table
 */
public class PutData {
        public static void main(String[] args) {
                Connection connection = HBaseConnect.getConnection();
                TableName tableName = TableName.valueOf("employee:staff1");

                try (Table table = connection.getTable(tableName)) {
                        Put put = new Put(Bytes.toBytes("staff001"));

                        // development_info 列族
                        put.addColumn(
                                        Bytes.toBytes("development_info"),
                                        Bytes.toBytes("staff_name"),
                                        System.currentTimeMillis(),
                                        Bytes.toBytes("zhangsan"));
                        put.addColumn(
                                        Bytes.toBytes("development_info"),
                                        Bytes.toBytes("staff_age"),
                                        System.currentTimeMillis(),
                                        Bytes.toBytes("26"));
                        put.addColumn(
                                        Bytes.toBytes("development_info"),
                                        Bytes.toBytes("staff_phone"),
                                        System.currentTimeMillis(),
                                        Bytes.toBytes("17664487906"));

                        // sale_info 列族
                        put.addColumn(
                                        Bytes.toBytes("sale_info"),
                                        Bytes.toBytes("staff_name"),
                                        System.currentTimeMillis(),
                                        Bytes.toBytes("wangwu"));
                        put.addColumn(
                                        Bytes.toBytes("sale_info"),
                                        Bytes.toBytes("staff_age"),
                                        System.currentTimeMillis(),
                                        Bytes.toBytes("26"));
                        put.addColumn(
                                        Bytes.toBytes("sale_info"),
                                        Bytes.toBytes("staff_phone"),
                                        System.currentTimeMillis(),
                                        Bytes.toBytes("17880657921"));

                        table.put(put);
                        System.out.println("数据插入成功");

                } catch (IOException e) {
                        System.err.println("数据插入失败: " + e.getMessage());
                        e.printStackTrace();
                } finally {
                        HBaseConnect.closeConnection();
                }
        }
}
