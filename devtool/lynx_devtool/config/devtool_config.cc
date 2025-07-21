// Copyright 2020 The Lynx Authors. All rights reserved.
// Licensed under the Apache License Version 2.0 that can be found in the
// LICENSE file in the root directory of this source tree.

#include "devtool/lynx_devtool/config/devtool_config.h"

namespace lynx {
namespace devtool {

std::atomic<bool> DevToolConfig::should_stop_at_entry_ = {false};
std::atomic<bool> DevToolConfig::should_stop_mts_at_entry_ = {false};
std::atomic<bool> DevToolConfig::should_fetch_mts_debug_info_ = {false};

void DevToolConfig::SetStopAtEntry(bool stop_at_entry, bool is_mts) {
  // If stopping at the entry is required, fetch the debug-info as well.
  if (stop_at_entry) {
    SetFetchDebugInfo(stop_at_entry, is_mts);
  }
  if (is_mts) {
    should_stop_mts_at_entry_ = stop_at_entry;
  } else {
    should_stop_at_entry_ = stop_at_entry;
  }
}

bool DevToolConfig::ShouldStopAtEntry(bool is_mts) {
  if (is_mts) {
    return should_stop_mts_at_entry_;
  }
  return should_stop_at_entry_;
}

void DevToolConfig::SetFetchDebugInfo(bool fetch, bool is_mts) {
  if (is_mts) {
    should_fetch_mts_debug_info_ = fetch;
  }
}

bool DevToolConfig::ShouldFetchDebugInfo(bool is_mts) {
  if (is_mts) {
    return should_fetch_mts_debug_info_;
  }
  return false;
}

}  // namespace devtool
}  // namespace lynx
