package com.facilcomanda.tableservice;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.openfeign.EnableFeignClients;
@EnableFeignClients(basePackages = "com.facilcomanda")
@SpringBootApplication(scanBasePackages = "com.facilcomanda")
public class TableServiceApplication { public static void main(String[] args) { SpringApplication.run(TableServiceApplication.class, args); } }
