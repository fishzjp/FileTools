# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.3] - 2025-12-20

### Updated
- 更新版本号至 1.0.3

## [0.2.0] - 2025-12-20

### Changed
- 重构项目目录结构，采用标准的 src-layout 布局
- 将源代码模块移动到 `src/filetools/` 目录
- 将所有文档整理到 `docs/` 目录
- 优化项目结构，符合开源项目规范

### Added
- 添加 `LICENSE` 文件（MIT 许可证）
- 添加 `CHANGELOG.md` 版本变更记录
- 添加 `.github/workflows/ci.yml` CI 工作流
- 添加 `assets/` 目录用于存放资源文件

### Updated
- 更新所有导入语句以适配新的包结构
- 更新 `pyproject.toml` 配置，添加完整的项目元数据
- 更新所有文档中的项目结构说明
- 更新所有文档中的日期为当前日期

## [0.1.0] - 2025-12-20

### Added
- 基于 Gradio 的现代化 Web 界面
- 文件大小生成功能（支持 KB/MB/GB/TB）
- 实时磁盘空间监控功能
- 完善的输入验证和错误处理
- 日志记录系统
- 单元测试覆盖
- 完整的项目文档

### Features
- 快速文件生成：使用块写入算法（100MB 块）提高生成速度
- 实时磁盘监控：显示所有磁盘分区的使用情况
- 智能错误处理：包括磁盘空间检查和友好的错误提示
- 跨平台支持：支持 Windows、macOS、Linux 系统

[Unreleased]: https://github.com/fishzjp/FileTools/compare/v1.0.3...HEAD
[1.0.3]: https://github.com/fishzjp/FileTools/compare/v0.2.0...v1.0.3
[0.2.0]: https://github.com/fishzjp/FileTools/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/fishzjp/FileTools/releases/tag/v0.1.0

