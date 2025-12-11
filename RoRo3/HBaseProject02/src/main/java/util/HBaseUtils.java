package util;

import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.util.Bytes;

import java.math.BigDecimal;

/**
 * HBase 数据读取工具类
 * 
 * 提供从 HBase Result 对象中读取不同类型数据的便捷方法
 * 避免在多个类中重复定义相同的工具方法
 */
public class HBaseUtils {

    /**
     * 从 Result 中读取 String 类型的列值
     * 
     * @param result    HBase 查询结果
     * @param cf        列族名
     * @param qualifier 列名
     * @return 列值，如果不存在返回 null
     */
    public static String getString(Result result, String cf, String qualifier) {
        byte[] value = result.getValue(Bytes.toBytes(cf), Bytes.toBytes(qualifier));
        return value == null ? null : Bytes.toString(value);
    }

    /**
     * 从 Result 中读取 BigDecimal 类型的列值
     * 
     * @param result    HBase 查询结果
     * @param cf        列族名
     * @param qualifier 列名
     * @return 列值，如果不存在返回 null
     */
    public static BigDecimal getBigDecimal(Result result, String cf, String qualifier) {
        byte[] value = result.getValue(Bytes.toBytes(cf), Bytes.toBytes(qualifier));
        return value == null ? null : Bytes.toBigDecimal(value);
    }

    /**
     * 从 Result 中读取 Long 类型的列值
     * 
     * @param result    HBase 查询结果
     * @param cf        列族名
     * @param qualifier 列名
     * @return 列值，如果不存在返回 null
     */
    public static Long getLong(Result result, String cf, String qualifier) {
        byte[] value = result.getValue(Bytes.toBytes(cf), Bytes.toBytes(qualifier));
        return value == null ? null : Bytes.toLong(value);
    }

    /**
     * 从 Result 中读取 Integer 类型的列值
     * 
     * @param result    HBase 查询结果
     * @param cf        列族名
     * @param qualifier 列名
     * @return 列值，如果不存在返回 null
     */
    public static Integer getInt(Result result, String cf, String qualifier) {
        byte[] value = result.getValue(Bytes.toBytes(cf), Bytes.toBytes(qualifier));
        return value == null ? null : Bytes.toInt(value);
    }

    /**
     * 从 Result 中读取 Double 类型的列值
     * 
     * @param result    HBase 查询结果
     * @param cf        列族名
     * @param qualifier 列名
     * @return 列值，如果不存在返回 null
     */
    public static Double getDouble(Result result, String cf, String qualifier) {
        byte[] value = result.getValue(Bytes.toBytes(cf), Bytes.toBytes(qualifier));
        return value == null ? null : Bytes.toDouble(value);
    }

    /**
     * 从 Result 中读取 byte[] 类型的列值
     * 
     * @param result    HBase 查询结果
     * @param cf        列族名
     * @param qualifier 列名
     * @return 列值，如果不存在返回 null
     */
    public static byte[] getBytes(Result result, String cf, String qualifier) {
        return result.getValue(Bytes.toBytes(cf), Bytes.toBytes(qualifier));
    }
}
