package com.tien;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import io.github.bonigarcia.wdm.WebDriverManager;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.List;
import java.util.Scanner;

public class ComicImageDownloader {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Nhập URL truyện (ví dụ: https://nettruyenvie.com/truyen-tranh/dao-hai-tac): ");
        String baseUrl = scanner.nextLine().trim();
        System.out.println("Nhập số chương muốn tải (tải từ chương 0 đến chương này):");
        int chapterCount = scanner.nextInt();
        downloadImages(baseUrl, false);
        for (int i = 0; i <= chapterCount; i++) {
            String chapterUrl = baseUrl + "/chuong-" + i;
            downloadImages(chapterUrl, true);
        }
        scanner.close();
    }

    public static void downloadImages(String url, boolean multipleImages) {
        String comicName = extractComicName(url);
        WebDriverManager.chromedriver().setup();
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless");
        options.addArguments("--disable-gpu");
        WebDriver driver = new ChromeDriver(options);

        try {
            driver.get(url);
            Thread.sleep(5000);
            File comicFolder = new File(comicName);
            if (!comicFolder.exists()) {
                comicFolder.mkdirs();
            }

            String chapterNumber = extractChapterNumber(url);
            String chapterFolderPath;

            if (multipleImages) {
                chapterFolderPath = comicName + File.separator + comicName + "-" + chapterNumber;
                File chapterFolder = new File(chapterFolderPath);
                if (!chapterFolder.exists()) {
                    chapterFolder.mkdirs();
                }
            } else {
                chapterFolderPath = comicName;
            }

            if (multipleImages) {
                List<WebElement> images = driver.findElements(By.cssSelector("img.lozad"));
                for (int idx = 0; idx < images.size(); idx++) {
                    String imgUrl = images.get(idx).getAttribute("data-src");
                    if (imgUrl != null && !imgUrl.isEmpty()) {
                        String imgName = comicName + "-" + chapterNumber + "-" + (idx + 1) + ".jpg";
                        String imgPath = chapterFolderPath + File.separator + imgName;
                        downloadAndSaveImage(imgUrl, imgPath, url);
                    }
                }
            } else {
                WebElement imgElement = driver.findElement(By.cssSelector("div.col-xs-4.col-image img.image-thumb"));
                String imgUrl = imgElement.getAttribute("data-src");
                if (imgUrl != null && !imgUrl.isEmpty()) {
                    String imgName = comicName + "-cover.jpg";
                    String imgPath = chapterFolderPath + File.separator + imgName;
                    downloadAndSaveImage(imgUrl, imgPath, url);
                }
            }
        } catch (Exception e) {
            System.out.println("Lỗi khi tải ảnh từ " + url + ": " + e.getMessage());
        } finally {
            driver.quit();
        }
    }

    public static void downloadAndSaveImage(String imgUrl, String imgPath, String refererUrl) {
        try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
            HttpGet request = new HttpGet(imgUrl);
            request.setHeader("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36");
            request.setHeader("Referer", refererUrl);

            try (CloseableHttpResponse response = httpClient.execute(request);
                 InputStream inputStream = response.getEntity().getContent();
                 FileOutputStream outputStream = new FileOutputStream(new File(imgPath))) {

                byte[] buffer = new byte[4096];
                int bytesRead;
                while ((bytesRead = inputStream.read(buffer)) != -1) {
                    outputStream.write(buffer, 0, bytesRead);
                }
                System.out.println("Đã tải " + imgPath + " thành công!");
            }
        } catch (IOException e) {
            System.out.println("Lỗi khi tải ảnh " + imgUrl + ": " + e.getMessage());
        }
    }

    private static String extractComicName(String url) {
        try {
            URI uri = new URI(url);
            String[] pathParts = uri.getPath().split("/");
            return pathParts.length > 2 ? pathParts[2] : "comic";
        } catch (URISyntaxException e) {
            return "comic";
        }
    }
    
    private static String extractChapterNumber(String url) {
        try {
            URI uri = new URI(url);
            String[] pathParts = uri.getPath().split("/");
            return pathParts.length > 1 ? pathParts[pathParts.length - 1] : "unknown";
        } catch (URISyntaxException e) {
            return "unknown";
        }
    }
}