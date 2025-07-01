-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 30, 2025 at 12:33 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `wahid_app`
--

-- --------------------------------------------------------

--
-- Table structure for table `barang`
--

CREATE TABLE `barang` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `harga` decimal(10,2) NOT NULL,
  `stok` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `barang`
--

INSERT INTO `barang` (`id`, `nama`, `harga`, `stok`) VALUES
(1, 'Laptop Lenovo Thinkpad', 9500000.00, 10),
(2, 'Mouse Logitech M170', 150000.00, 30),
(3, 'Keyboard Mechanical Rexus', 350000.00, 20),
(4, 'Monitor LG 24 inch', 1850000.00, 15),
(5, 'Printer Epson L3110', 2200000.00, 7),
(6, 'Harddisk Eksternal 1TB', 750000.00, 24),
(7, 'Flashdisk Sandisk 32GB', 65000.00, 50),
(8, 'Speaker Bluetooth JBL', 450000.00, 12),
(9, 'Router TP-Link AC1200', 375000.00, 17),
(10, 'Webcam Logitech C270', 600000.00, 10);

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `alamat` text DEFAULT NULL,
  `telepon` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`id`, `nama`, `alamat`, `telepon`) VALUES
(1, 'Andi Pratama', 'Jl. Merdeka No. 1', '081234567890'),
(2, 'Budi Santoso', 'Jl. Ahmad Yani No. 45', '082234567891'),
(3, 'Citra Dewi', 'Jl. Kartini No. 78', '083334567892'),
(4, 'Dian Permata', 'Jl. Cendrawasih No. 5', '084434567893'),
(5, 'Eka Ramadhan', 'Jl. Sudirman No. 13', '085534567894'),
(6, 'Fajar Hidayat', 'Jl. Asia Afrika No. 88', '086634567895'),
(7, 'Gita Larasati', 'Jl. Kebon Jeruk No. 23', '087734567896'),
(8, 'Hendra Wijaya', 'Jl. Diponegoro No. 12', '088834567897'),
(9, 'Septian', 'Jl. Kenanga No. 02', '089777888999'),
(10, 'Arman', 'Jl. Kenanga No. 03', '897778880001');

-- --------------------------------------------------------

--
-- Table structure for table `pengguna`
--

CREATE TABLE `pengguna` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `role` enum('admin','user') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pengguna`
--

INSERT INTO `pengguna` (`id`, `username`, `password`, `role`) VALUES
(1, 'admin', 'admin123', 'admin'),
(2, 'user', 'userpass', 'user');

-- --------------------------------------------------------

--
-- Table structure for table `transaksi`
--

CREATE TABLE `transaksi` (
  `id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `barang_id` int(11) DEFAULT NULL,
  `jumlah` int(11) DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  `tanggal` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transaksi`
--

INSERT INTO `transaksi` (`id`, `customer_id`, `barang_id`, `jumlah`, `total`, `tanggal`) VALUES
(1, 1, 1, 1, 9500000.00, '2025-06-01 10:00:00'),
(2, 2, 3, 2, 700000.00, '2025-06-02 11:30:00'),
(3, 3, 6, 1, 750000.00, '2025-06-03 09:45:00'),
(4, 4, 2, 3, 450000.00, '2025-06-04 13:15:00'),
(5, 5, 5, 1, 2200000.00, '2025-06-05 15:20:00'),
(6, 6, 8, 2, 900000.00, '2025-06-06 16:00:00'),
(7, 1, 1, 1, 9500000.00, '2025-06-01 10:00:00'),
(14, 7, 6, 1, 750000.00, '2025-06-29 16:19:59'),
(15, 9, 5, 1, 2200000.00, '2025-06-29 18:37:40'),
(16, 8, 9, 1, 375000.00, '2025-06-29 19:08:44');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `barang`
--
ALTER TABLE `barang`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pengguna`
--
ALTER TABLE `pengguna`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `barang_id` (`barang_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `barang`
--
ALTER TABLE `barang`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `pengguna`
--
ALTER TABLE `pengguna`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `transaksi`
--
ALTER TABLE `transaksi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD CONSTRAINT `transaksi_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`),
  ADD CONSTRAINT `transaksi_ibfk_2` FOREIGN KEY (`barang_id`) REFERENCES `barang` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
